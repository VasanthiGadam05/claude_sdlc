---
name: confluence-fetch
description: Fetch a Confluence page's content by URL or ID and return it as normalized plain text. Use this whenever a command needs the source user story (Phase 1 / /requirements), rather than calling Atlassian tools directly.
---

# Confluence Fetch

Given a Confluence page reference (either a full URL like
`https://<site>.atlassian.net/wiki/spaces/.../pages/<id>/...` or a bare page ID), retrieve the page
and return its text content, stripped of storage-format markup.

## Steps

1. If given a URL, extract the numeric page ID from it (the segment after `/pages/`). If given a
   bare ID or a tiny-link code, use it as-is.
2. If no cloudId is already known in this session, call `getAccessibleAtlassianResources` first.
3. Call `getConfluencePage` with the resolved `cloudId` and `pageId`, `contentFormat: "markdown"`.
4. Return the page `title` and the markdown body as plain text. Do not summarize or truncate —
   the calling command needs the full story to write accurate requirements.
5. If the page can't be found or access is denied, report that clearly rather than guessing at a
   different page — stop and let the calling command ask the user to double check the reference.

## Notes

- Never invent a page ID or URL. If the caller doesn't have one, it must ask the user.
- This skill only reads Confluence; it never writes/comments/updates a page.
