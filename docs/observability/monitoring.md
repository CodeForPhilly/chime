# Monitoring for Chime

This outlines how to get access to both Application Logs, and logs for k8s cluster running Chime.

## Components

 - ElasticSearch is used as your data management system.
 - Fluentd will gather various log streams across the containers.
 - Kibana can be used to visualize those logs.

Derived from [EFK](https://github.com/kubernetes/kubernetes/tree/master/cluster/addons/fluentd-elasticsearch)