# Elastic APM

This application has been instrumented with Elastic APM. 

In order to [configure](https://www.elastic.co/guide/en/apm/agent/python/current/configuration.html) this application environment variables should be 
used in the configMap of the `app.yaml` file.


Custom instrumentation begins in the main method in `st_app.py` with the call

```
client = Client()
client.begin_transaction('main_page')
```
and ends with `client.end_transaction('main_page')`

The sidebar menu and charts are instrumented with [custom instrumentations](https://www.elastic.co/guide/en/apm/agent/python/current/api.html). 


The `display_sidebar` has its internal functions instrumented
with the `with` notation.

The `charts` and `display_header` are instrumented with the `annotation` method. 