## Overview
Implement the Confluence REST API v2 Label endpoints using the `/implement-method ${API_DOC_URL}` Claude Code slash command.

## API Endpoints to Implement

### 1. Get Labels (GET /labels)
- **URL**: https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-label/#api-labels-get
- **Description**: Returns all labels that exist across all pages, blogposts, whiteboards, databases, smart links, and folders in the Confluence instance

### 2. Get Page Labels (GET /pages/{id}/labels)
- **URL**: https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-label/#api-pages-id-labels-get
- **Description**: Returns the labels of a specific page

### 3. Get Space Labels (GET /spaces/{id}/labels)
- **URL**: https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-label/#api-spaces-id-labels-get
- **Description**: Returns the labels of a specific space

## Implementation Steps
For each API endpoint, use the slash command:
```
/implement-method ${API_DOC_URL}
```

Where `${API_DOC_URL}` is the respective Atlassian documentation URL for each endpoint.