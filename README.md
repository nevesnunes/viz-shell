# viz-shell

Notebook interface for interactive visualizations.

Currently it's only a prototype for generating visualizations via HTTP requests.

### Examples

```bash
./server.py

curl 'http://localhost:3100/csv' -F 'file=@static/matrix.csv'

# Adapted from: https://github.com/nevesnunes/aggregables#line-chart
curl 'http://localhost:3100/csv?type=line' -F 'file=@-' < ./static/instrace-filtered.log
```
