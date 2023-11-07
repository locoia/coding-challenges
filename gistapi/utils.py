import asyncio
from http import HTTPStatus

import aiohttp

from .models import Gist


async def fetch_gist_content(session, gist: Gist, compiled_pattern):
    # Asynchronously fetches and searches each file content within a given gist for the compiled_pattern.
    # Returns the gist URL if any file content matches the pattern, None otherwise.
    for file_info in gist.files.values():
        raw_url = file_info.raw_url
        async with session.get(raw_url) as file_response:
            if file_response.status == HTTPStatus.OK:
                async for chunk in file_response.content.iter_chunked(
                    1024 * 1024
                ):  # 1 MB chunks
                    if compiled_pattern.search(chunk.decode()):
                        return gist.url
    return None


async def fetch_gists(
    session, gists_url, compiled_pattern, logger, page=1, max_page=None
):
    # Paginates through all gists for a user and collects those that contain a match for the compiled_pattern.
    # GitHub API rate limiting errors are logged and raised.
    matches = []
    while max_page is None or page <= max_page:  # Pagination control
        params = {"page": page}
        async with session.get(gists_url, params=params) as response:
            if response.status == HTTPStatus.FORBIDDEN:
                # Rate limit detection; log and cease execution to prevent further limit exhaustion.
                logger.error("GitHub API rate limit exceeded")
                raise RuntimeError("GitHub API rate limit exceeded")
            elif response.status != HTTPStatus.OK:
                # Log any other HTTP errors encountered during gist fetching.
                error_msg = f"HTTP Error: {response.status} for URL {response.url}"
                logger.error(error_msg)
                raise aiohttp.ClientError(error_msg)

            gists_data = await response.json()
            if not gists_data:
                break  # Exit the loop if no more gists are available.

            gists = [Gist(**gist_data) for gist_data in gists_data]
            tasks = [
                fetch_gist_content(session, gist, compiled_pattern) for gist in gists
            ]
            # Aggregate results, filter out exceptions and None values.
            page_results = await asyncio.gather(*tasks, return_exceptions=True)
            matches.extend([match for match in page_results if match])

            logger.info(f"Page {page}: Retrieved {len(gists)} gists.")

            page += 1

    return matches
