# APIs pagination

All APIs that return a list of resources are paginated.

Sometimes, the returned result spans many pages. When listing resources, you can pass the following parameters :

| Parameter | Description |
|:----------|:------------|
| `page`     | Page number (default: `1`) |
| `per_page` | Number of items to list per page (default: `20`, max: `50`) |

In the following example, we list `50` incidents per page:

```shell
curl --request GET "https://localhost:8080/api/incident?per_page=50"
```

## Pagination headers

In order to help with the pagination, custom HTTP headers are provided :

| Header | Description |
|:-------|:------------|
| `x-next-page`   | The index of the next page |
| `x-page`        | The index of the current page (starting at `1`) |
| `x-per-page`    | The number of items per page |
| `x-prev-page`   | The index of the previous page |
| `x-total`       | The total number of items |
| `x-total-pages` | The total number of pages |

**NB:** `x-prev-page` and `x-next-page` could contains the value `None` if thoses pages don't exists.