# Standard Ebooks Downloader

A lightweight Python script that automatically generates official download URLs for books on [Standard Ebooks](https://standardebooks.org/), downloads the uncorrupted `.epub` file directly to a local subfolder, and opens the directory automatically for easy uploading to Kindle.

This workflow skips programmatic email pipelines (`smtplib`), bypassing the common Amazon `E999 Send to Kindle Internal Error` server bugs by allowing clean, manual drag-and-drop ingestion via [amazon.com/sendtokindle](https://www.amazon.com/sendtokindle).

## Features

- **Exact Matching:** Extracts and preserves the exact filename used by Standard Ebooks servers.
- **Auto-Organization:** Automatically creates and downloads books into a dedicated `/downloads` folder.
- **Workflow Automation:** Automatically launches Windows Explorer pointed directly at your new download.

## Prerequisites

Make sure you have the Python `requests` library installed:

```bash
pip install requests