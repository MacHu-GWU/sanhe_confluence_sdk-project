.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.1.2 (2026-01-05)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add folder management APIs: ``CreateFolderRequest``, ``GetFolderRequest``, ``DeleteFolderRequest``
- Add children APIs: ``GetDirectPageChildrenRequest``, ``GetFolderDirectChildrenRequest``
- Add descendant APIs: ``GetPageDescendantsRequest``, ``GetFolderDescendantsRequest``

**Minor Improvements**

- Improved ``gen_m.py`` code generator to also export parameter classes (``RequestPathParams``, ``RequestQueryParams``, ``RequestBodyParams``) in ``m.py``


0.1.1 (2025-12-30)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First release
- Add space APIs: ``GetSpacesRequest``, ``GetSpaceRequest``, ``CreateSpaceRequest``
- Add page APIs: ``GetPagesRequest``, ``GetPageRequest``, ``CreatePageRequest``, ``UpdatePageRequest``, ``DeletePageRequest``, ``GetPagesInSpaceRequest``, ``GetPagesForLabelRequest``, ``UpdatePageTitleRequest``
- Add label APIs: ``GetLabelsRequest``, ``GetLabelsForPageRequest``, ``GetLabelsForSpaceRequest``
- Add pagination utility: ``paginate()`` function for iterating through paginated list endpoints
