# viz-shell

Apply transformations to datasets by manipulating interactive visualizations.

### Roadmap

Currently it's only a prototype for generating visualizations via HTTP requests.

Use case to support:

1. Submit input to visualize;
2. Apply manual transformation to visualization, resulting in a new dataset;
3. Export both the new dataset (same format as input) and a recording of applied transformations;
4. Automate this process for the next inputs, by being able to replay the recorded transformations in a script.

### Examples

```bash
./server.py

curl 'http://localhost:3100/csv' -F 'file=@static/matrix.csv'

# Adapted from: https://github.com/nevesnunes/aggregables#line-chart
curl 'http://localhost:3100/csv?type=line' -F 'file=@-' < ./static/instrace-filtered.log
```
