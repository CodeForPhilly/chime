# Helm

The directory holds the values.yaml for deploying various pre-defined helm charts can be found in `k8s/helm/` 

First off lets assume that helm has already been deployed. 

To install a helm chart it's quite simple:

```
helm install --name deployment_name --namespace somenamespace chart/name
```

If we want to specify some overrides to that charge we can specify those as cli arguments, 
or "more better" we can specify those in values.yaml file. 

```
helm install -f path/to/values.yaml --name deployment_name --namespace somenamespace chart/name
```

## Elasticsearch

First off lets deploy Elasticsearch using the 
[official helm chart](https://github.com/elastic/helm-charts/tree/master/elasticsearch). 

If you haven't added the elastic helm repo you should do that first:

```
helm repo add elastic https://helm.elastic.co
```

If you want to practice installing Elasticsearch you can specify a new namespace and delete it when you're done. 

Next let's assume we want to deploy elasticsearch to a testing namespace. Lets call it `test-es`

```
$ helm install --name elasticsearch --namespace test-es elastic/elasticsearch
```

Now you can monitor the pods to see if elasticearch is up and ready. 

Now lets say we want to make some changes to the options for deploying elasticsearch. 
You can create a file in `values` called `Elasticsearch.yaml`. And to deploy these changes
we just need to run the command: 

```
$ helm upgrade -f values/elasticsearch.yaml elasticsearch elastic/elasticsearch --namespace test-es
```

The upgrade process will 1 by 1 take add a new elasticsearch node in to the cluster, wait till the cluster is green
then remove a node from the cluster, wait till green and so on. 

The upgrade of elasticsearch can be done with 0 downtime using this rolling upgrade procedure. 

This processss can also be used to upgrade elasticsearch to newer versions in the future. 

## Kibana

Deploying kibana is just as simple as deploying elasticsearch. 

Skipping the initial install step like we did with Elasticsearch, lets assume that we already have the values file
for kibana we wanna use. 

So deploying kibana using a custom values file can be done using: 

```
helm upgrade -i -f values/kibana.yaml --name kibana --namespace test-es elastic/kibana
```

We'll note here that this command is slightly different. In this case we are running `upgrade` with the `-i` flag. 
This means upgrade if a release exists already, if not install it. This command is more idempotent than the first
command we saw in the [Elasticsearch](./README.md#elasticsearch) section.

### Ingress

Please note that by default the Ingress for Kibana is disabled. 
If you'd like to enable the ingress for Kibana you must do so explicitly. 

The default configuration for kibana can be found [here](https://github.com/elastic/helm-charts/blob/master/kibana/values.yaml#L105-L116)

In the `values/kibana.yaml` file you must override the Ingress settings to enable an ingress for Kibana. 

### Port Forwarding

In the meantime after kibana has been deployed you can use kubectl's port forwarding to be able to access kibana
instance using localhost. 

```
$ kubectl port-forward deployment/kibana-kibana 5601 -n test-es
```

Now you can access kibana through `http://localhost:5601`


## APM Server

Deploying the APM server using a custom values.yaml file would look like: 

```
helm upgrade -i -f values/apm-server.yaml --name apm-server --namespace test-es elastic/apm-server
```

Like Kibana the APM server is configured without an ingress. This should not be exposed publicly, except in the case
where you want to collect APM data from an application that's running outside of the k8s cluster. 
Even in that event, I would suggest, deploying that app to k8s instead. 

## Beats

Deploying the metricbeats and filebeats using a custom values.yaml file would look like: 

```
helm upgrade -i -f values/filebeat.yaml --name filebeat --namespace test-es elastic/filebeat
helm upgrade -i -f values/metricbeat.yaml --name metricbeat --namespace test-es elastic/metricbeat
```

Metricbeat and filebeat are both configured by default to start pulling metrics/logs from the k8s cluster and ship to the local Elasticsearch instance. 

