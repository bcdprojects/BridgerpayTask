# BridgerPay Task

## **Question 1**

### 1. a GKE cluster with a node pool of size 3 and n1-standard-2 machine types

> https://console.cloud.google.com/kubernetes/clusters/

### 2. Installing ECK using the Helm chart onto the GKE cluster

```
- helm repo add elastic https://helm.elastic.co
- helm repo update
- helm install elastic-operator elastic/eck-operator -n elk --create-namespace
- kubectl get all -n elk
```

### 3. Creatin the ElasticSearch

```
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: bcdbridgerpayelasticsearch
spec:
  version: 7.6.2
  nodeSets:
  - name: default
    count: 1
    config:
      node.master: true
      node.data: true
      node.ingest: true
      node.store.allow_mmap: false
```

### 4. Creatin the Kibaba

```
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: bcdkb
spec:
  version: 7.6.2
  count: 1
  elasticsearchRef:
    name: bcdbridgerpayelasticsearch
```

### 5. Checking if everything is OK

    `kubectl get elastic`
    ```
    rachel33118301@cloudshell:~ (inner-domain-328310)$ kubectl get elastic
    W0613 23:03:03.142891     560 gcp.go:120] WARNING: the gcp auth plugin is deprecated in v1.22+, unavailable in v1.25+; use gcloud instead.
    To learn more, consult https://cloud.google.com/blog/products/containers-kubernetes/kubectl-auth-changes-in-gke
    NAME                                                                    HEALTH   NODES   VERSION   PHASE   AGE
    elasticsearch.elasticsearch.k8s.elastic.co/bcdbridgerpayelasticsearch   green    1       7.6.2     Ready   8h

    NAME                                 HEALTH   NODES   VERSION   AGE
    kibana.kibana.k8s.elastic.co/bcdkb   green    1       7.6.2     3h47m
    ```

## **Question 2**

### 1.  Access the Elasticsearch from within the cluster using the service bcdbridgerpayelasticsearch-es-http at port 9200.

    ```
    kubectl port-forward service/bcdbridgerpayelasticsearch-es-http 9200
    W0613 23:56:05.280870     572 gcp.go:120] WARNING: the gcp auth plugin is deprecated in v1.22+, unavailable in v1.25+; use gcloud instead.
    To learn more, consult https://cloud.google.com/blog/products/containers-kubernetes/kubectl-auth-changes-in-gke
    **Forwarding from 127.0.0.1:9200 -> 9200**
    ```

### 2. Creatin a Secret:

    ##### a. Creating a Password - base64
    
    I ran `kubectl get secret bcdbridgerpayelasticsearch-es-elastic-user -o=jsonpath='{.data.elastic}' | base64 --decode`
    and got this password:
    `FEH837Ac30uJLT2126z7Igto`
    
    ![the screen after the login screan](https://s20.directupload.net/images/220614/8qb8l9fs.png)
    

then I added LoadBalancer to the Kibana:

```
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: bcdkb
spec:
  version: 7.6.2
  count: 1
  elasticsearchRef:
    name: bcdbridgerpayelasticsearch
  http:
    service:
        spec:
            type: LoadBalancer
```
and when I ran `kubectl get all` I got:

```
...
service/bcdkb-kb-http                                  LoadBalancer   10.52.4.201    35.225.117.253   5601:31609/TCP   11h
...
```
then- I could populated access the Kibana UI:

`https://35.202.76.151:5601`

and I entered with the username and the password


now I created Ingress with Secret and IngressClass:

```
apiVersion: networking.k8s.io/v1
kind: IngressClass
metadata:
  labels:
    app.kubernetes.io/component: controller
  name: bcdbcdbcdingressclassbcdbcdbcd
  annotations:
    ingressclass.kubernetes.io/is-default-class: "true"
spec:
  controller: k8s.io/ingress-nginx


```
```
apiVersion: v1
kind: Secret
metadata:
  name: bcd-kibana-testsecret-tls
  namespace: default
type: kubernetes.io/tls
data:
  tls.crt: |
          LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUREVENDQWZXZ0F3SUJBZ0lVVkk1ellBakR0
          RWFyd0Zqd2xuTnlLeU0xMnNrd0RRWUpLb1pJaHZjTkFRRUwKQlFBd0ZqRVVNQklHQTFVRUF3d0xa
          bTl2TG1KaGNpNWpiMjB3SGhjTk1qSXdOakUxTVRJeE16RTVXaGNOTWpNdwpOakUxTVRJeE16RTVX
          akFXTVJRd0VnWURWUVFEREF0bWIyOHVZbUZ5TG1OdmJUQ0NBU0l3RFFZSktvWklodmNOCkFRRUJC
          UUFEZ2dFUEFEQ0NBUW9DZ2dFQkFLMVRuTDJpZlluTUFtWEkrVmpXQU9OSjUvMGlpN0xWZlFJMjQ5
          aVoKUXl5Zkw5Y2FQVVpuODZtY1NSdXZnV1JZa3dLaHUwQXpqWW9aQWR5N21TQ3ROMmkzZUZIRGdq
          NzdZNEhQcFA1TQpKVTRzQmU5ZmswcnlVeDA3aU11UVA5T3pibGVzNHcvejJIaXcyYVA2cUl5ZFI3
          bFhGSnQ0NXNSeDJ3THRqUHZCClErMG5UQlJrSndsQVZQYTdIYTN3RjBTSDJXL1dybTgrNlRkVGpG
          MmFUanpkMFFXdy9hKzNoUU9HSnh4b1JxY1MKYmNNYmMrYitGeCtqZ3F2N0xuQ3R1Njd5L2tsb3ZL
          Z2djdW41ZVNqY3krT0ZpdTNhY2hLVDlUeWJlSUxPY2FSYQp3KzJSeitNOUdTMWR2aUI0Q0dRNnlw
          RDhkazc4bktja1FBam9QMXV5ZXJnR2hla0NBd0VBQWFOVE1GRXdIUVlEClZSME9CQllFRkpLUWps
          KzI0TVJrNVpqTlB4ZVRnVU1pbE5xWk1COEdBMVVkSXdRWU1CYUFGSktRamwrMjRNUmsKNVpqTlB4
          ZVRnVU1pbE5xWk1BOEdBMVVkRXdFQi93UUZNQU1CQWY4d0RRWUpLb1pJaHZjTkFRRUxCUUFEZ2dF
          QgpBSUp2Y1ZNclpEUEZ6TEhvZ3IyZklDN0E0TTB5WFREZXhONWNEZFFiOUNzVk0zUjN6bkZFU1Jt
          b21RVVlCeFB3CmFjUVpWQ25qM0xGamRmeExBNkxrR0hhbjBVRjhDWnJ4ODRRWUtzQTU2dFpJWFVm
          ZXRIZk1zOTZsSE5ROW5samsKT3RoazU3ZkNRZVRFMjRCU0RIVDJVL1hhNjVuMnBjcFpDU2FYWStF
          SjJaWTBhZjlCcVBrTFZud3RTQ05lY0JLVQp3N0RCM0o4U2h1Z0FES21xU2VJM1R2N015SThvNHJr
          RStBdmZGTUw0YlpFbS9IWW4wNkxQdVF3TUE1cndBcFN3CnlDaUJhcjRtK0psSzNudDRqU0hGeU4x
          N1g1M1FXcnozQTNPYmZSWXI0WmJObE8zY29ObzFiQnd3eWJVVmgycXoKRGIrcnVWTUN5WjBTdXlE
          OGZURFRHY1E9Ci0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0K
  tls.key: |
          LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tCk1JSUV2UUlCQURBTkJna3Foa2lHOXcwQkFRRUZB
          QVNDQktjd2dnU2pBZ0VBQW9JQkFRQ3RVNXk5b24ySnpBSmwKeVBsWTFnRGpTZWY5SW91eTFYMENO
          dVBZbVVNc255L1hHajFHWi9PcG5Fa2JyNEZrV0pNQ29idEFNNDJLR1FIYwp1NWtnclRkb3QzaFJ3
          NEkrKzJPQno2VCtUQ1ZPTEFYdlg1Tks4bE1kTzRqTGtEL1RzMjVYck9NUDg5aDRzTm1qCitxaU1u
          VWU1VnhTYmVPYkVjZHNDN1l6N3dVUHRKMHdVWkNjSlFGVDJ1eDJ0OEJkRWg5bHYxcTV2UHVrM1U0
          eGQKbWs0ODNkRUZzUDJ2dDRVRGhpY2NhRWFuRW0zREczUG0vaGNmbzRLcit5NXdyYnV1OHY1SmFM
          eW9JSExwK1hrbwozTXZqaFlydDJuSVNrL1U4bTNpQ3puR2tXc1B0a2MvalBSa3RYYjRnZUFoa09z
          cVEvSFpPL0p5bkpFQUk2RDliCnNucTRCb1hwQWdNQkFBRUNnZ0VCQUpyb3FLUy83aTFTM1MyMVVr
          MTRickMxSkJjVVlnRENWNGk4SUNVOHpWRzcKTUZteVJPT0JFc0FiUXlmd1V0ZXBaaktxODUwc3Rp
          cWZzUTlqeHpieU9SeHBKYXNGN29sMXluaUJhYmd4dkFIQwp6TWNsQjVLclEyZFVCeTNRVFl0YXla
          cW9sUU56NzV2bWk0M0lBQTQwbjU3aFdqU2QrTG5IL0hNQWRzbW04SnVwCjA5d3VHMGltdEhQYm5B
          TERnY2N3V04zY2xxU0FtR3pxbW9kOEE1YjBWZTQwZHhjTXh3TldaN0JqOTBnamNWYnQKVU1aaFhp
          T2E2bnNSSHZDQjF0b0lmZVBuOEdzRk9nOUVqUHZDTWM4QWZKVW84Qk5TK2N0RmF3RjRWaUUyUHlB
          VgpxZzR1MHhBQ2Qya28zUUtpZFpsbjAyZkc2ZWg1UmxGYzdsL1RiWWxQY2xFQ2dZRUEyU0NvK2pJ
          MUZ1WkZjSFhtCm1Ra2Z3Q0Vvc28xd3VTV3hRWDBCMnJmUmJVbS9xdXV4Rm92MUdVc0hwNEhmSHJu
          RWRuSklqVUw4bWxpSjFFUTkKVUpxZC9SVkg1OTdZZ2Zib1dCbHh0cVhIRFRObjNIU3JzQmJlQTh6
          NXFMZjE2QzZaa3U3YmR3L2pxazJVaFgrcwp6T3piYTVqYVVYU0pXYXpzRmZoZjdSMlZ3UTBDZ1lF
          QXpGdDZBTDNYendBSi9EcXU5QlVuaTIxemZXSUp5QXFwCnBwRnNnQUczVkVYZWFRMjVGcjV6cURn
          dlBWRkF5QUFYMU9TL3pHZVcxaDQ0SERzQjRrVmdxVlhHSTdoQUV1RjYKRlgra1M5Uk5QdmFsYXdQ
          cXp4VTdPQmcvUis5NVB1NW1oNnFrRWVUekM2T21ZUGRGbmVQcWxKZk03YU43OEhjOApGVU1xRTBa
          NkNVMENnWUJJUUVYNmU1cU85REZIS3ZTQkdEZ29odUEwQ2p6b1gxS01xRHhsdTZWRTZMV08rcjhD
          CjhhK3Rxdm54RTVaYmN4V2RGSXB2OTBwM1VkOExjMm16MkwrWjUrcjFqWUllUFRzemxjUHhNMWo1
          VzVIRUdrN0gKV2RTbkR4NUV0bkp0d0pQNkFPR216UExGU091VFFOa1BtQUdyM0VGSnVhMjYyWC8y
          RDZCY0Z1d3VRUUtCZ0V0aApHcm1YVFRsdnZEOHJya2tlWEgzVG01d09RNmxrTlh2WmZIb2pKK3FQ
          OHlBeERhclVDWGx0Y0E5Z0gxTW1wYVBECjFQT2k2a0tFMXhHaXVta3FTaU5zSGpBaTBJK21XQkFD
          Q3lwbFh6RHdiY2Z4by9WSzBaTTVibTRzYVQ3TFZVcUoKcVFkb3VqWDY0VzQzQjVqYjd6VnNZUXp2
          RnRKMlNOVlc5dmd4TU9hcEFvR0FDaHphN3BMWWhueFA5QWVUL1pxZwpvUWM0ckh1SDZhTDMveCtq
          dlpRVXdiSitKOWZGY05pcTFZRlJBL2RJSEJWcGZTMWJWR3N3OW9MT2tsTWxDckxRCnJKSjkzWlRu
          dFdSQ1FCOTNMbXhoZmJuRk9CemZtbHZYTjFJeE1FNStVbVZRQmRLaS9YMktMZnFSUW5HVTExL2UK
          NytFcXFFbllrWTBraE1HL0xqRlRTU0E9Ci0tLS0tRU5EIFBSSVZBVEUgS0VZLS0tLS0K
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: tls-bcd-ingress-bcdmmm
spec:
  ingressClassName: bcdbcdbcdingressclassbcdbcdbcd
  tls:
  - hosts:
      -  kibana.example.com
    secretName: bcdsecret
  rules:
  - host: kibana.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: quickstartcd-kb-http
            port:
              number: 5601

```

## **Question 3**

Creating a new storage class object to utilize SSD persistent disks:

```
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: faster
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-ssd

```

Creating a persistent volume claim for MySQL:

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pvc
spec:
  storageClassName: faster
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 30Gi
```
`kubectl apply -f mysql-pvc.yml`

>persistentvolumeclaim/mysql-pvc created

Creating a new base64 encoded password:
`echo -n mypassword | base64 -w 0`

I got: `bXlwYXNzd29yZA==`

So I put this in the Secret:
```
apiVersion: v1
kind: Secret
metadata:
  name: mysql
data:
  password: bXlwYXNzd29yZA==
```
>secret/mysql created

![The storage](https://mail.google.com/mail/u/0?ui=2&ik=fb202b4c3e&attid=0.1&permmsgid=msg-a:r-4149464159858431159&th=1816dc98a59e6753&view=fimg&fur=ip&sz=s0-l75-ft&attbid=ANGjdJ9otQNB-StIN1ETFVVSt3pkLuxF3d8MOigX0wwSikJ2ZYbxYgSVeu2i3dCoE8Zj9EDZHPJKwiRHkROqAY5LYVEj6aitYaGGFgiCuabdJEdAsXlTBaMDVCfhv68&disp=emb&realattid=ii_l4hczvge0)

Creating the database namespace:
```
apiVersion: v1
kind: Namespace
metadata:
  name:  database 
```
Creating the MySql deployment and specifying node via setting **nodeAffinity**:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql
  namespace: database 
  labels:
    app: mysql
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: disktype
                operator: In
                values:
                - ssd
      containers:
        - image: mysql:5.6
          name: mysql
          env:
            - name: MYSQL_ROOT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: mysql
                  key: password
          ports:
            - containerPort: 3306
              name: mysql
          volumeMounts:
            - name: mysql-persistent-storage
              mountPath: /var/lib/mysql
      volumes:
        - name: mysql-persistent-storage
          persistentVolumeClaim:
            claimName: mysql-pvc

```
## **Question 4**

Creating 2 namespaces:
```
apiVersion: v1
kind: Namespace
metadata:
  name:  client-a 
---

apiVersion: v1
kind: Namespace
metadata:
  name:  client-b 
```

### **Question 4.1**
Creating 2 services and 2 deployments:

First- I added this annotation in the Secret and in the MySQL Service So that Wordpresses can communicate with it:

```
  annotations:
    replicator.v1.mittwald.de/replicate-from: client-a/source-mysql,client-b/source-mysql
```
```
  annotations:
    replicator.v1.mittwald.de/replicate-from: client-a/mysql-service,client-b/mysql-service
```

Secound:
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wordpress
  namespace: client-a
  labels:
    app: wordpress
spec:
  selector:
    matchLabels:
      app: wordpress
  template:
    metadata:
      labels:
        app: wordpress
    spec:
      containers:
      - image: wordpress:5.9.3
        name: wordpress
        env:
        - name: WORDPRESS_DB_HOST
          value: mysql-service
        - name: WORDPRESS_DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: source-mysql
              key: password
        ports:
        - containerPort: 80
          name: wordpress
        volumeMounts:
        - name: wordpress-persistent-storage
          mountPath: /var/www/html
      volumes:
      - name: wordpress-persistent-storage
        persistentVolumeClaim:
          claimName: wordpress-pvc
```
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wordpress
  namespace: client-b
  labels:
    app: wordpress
spec:
  selector:
    matchLabels:
      app: wordpress
  template:
    metadata:
      labels:
        app: wordpress
    spec:
      containers:
      - image: wordpress:5.8
        name: wordpress
        env:
        - name: WORDPRESS_DB_HOST
          value: mysql-service
        - name: WORDPRESS_DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: source-mysql
              key: password
        ports:
        - containerPort: 80
          name: wordpress
        volumeMounts:
        - name: wordpress-persistent-storage
          mountPath: /var/www/html
      volumes:
      - name: wordpress-persistent-storage
        persistentVolumeClaim:
          claimName: wordpress-pvc
```
Services:
```
apiVersion: v1
kind: Service
metadata:
  name: wordpress-service
  namespace: client-a
spec:
  selector:
    app: wordpress
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: LoadBalancer
---
apiVersion: v1
kind: Service
metadata:
  name: wordpress-service
  namespace: client-b
spec:
  selector:
    app: wordpress
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: LoadBalancer
```
Criating 2 ingresses and 2 ingressClasses:

First I created one Secret Which connects to the two Ingresses by this:

```
  annotations:
    replicator.v1.mittwald.de/replicate-from: client-a/secret-wordpress-a,client-b/secret-wordpress-b
```

```
apiVersion: v1
kind: Secret
metadata:
  name: secret-wordpress-a
  namespace: default
  annotations:
    replicator.v1.mittwald.de/replicate-from: client-a/secret-wordpress-a,client-b/secret-wordpress-b
type: kubernetes.io/tls
data:
  tls.crt: crt.pem
  tls.key: key.pem
```

and then I created the two Ingresses:

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-wordpress-a
  namespace: client-a
spec:
  tls:
  - hosts:
      - wp01.example.com
    secretName: secret-wordpress-a
  rules:
  - host: wp01.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: wordpress-service
            port:
              number: 80
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-wordpress-b
  namespace: client-b
spec:
  tls:
  - hosts:
      - wp02.wordpress 
    secretName: secret-wordpress-a
  rules:
  - host: wp02.wordpress 
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: wordpress-service
            port:
              number: 80
```

and two ingressclasses:

```
apiVersion: networking.k8s.io/v1
kind: IngressClass
metadata:
  labels:
    app.kubernetes.io/component: controller
  name: wpa
  namespace: client-a
  annotations:
    ingressclass.kubernetes.io/is-default-class: "true"
spec:
  controller: k8s.io/ingress-nginx
---
apiVersion: networking.k8s.io/v1
kind: IngressClass
metadata:
  labels:
    app.kubernetes.io/component: controller
  name: wpb
  namespace: client-b
  annotations:
    ingressclass.kubernetes.io/is-default-class: "true"
spec:
  controller: k8s.io/ingress-nginx
```






## **Question 5**

Creating 2 HorizontalPodAutoscaler for each worddpress deployment:

```
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: hpa-wordpress
  namespace: client-a
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: wordpress
  minReplicas: 1
  maxReplicas: 5
  targetCPUUtilizationPercentage: 10
---
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: hpa-wordpress
  namespace: client-b
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: wordpress
  minReplicas: 1
  maxReplicas: 5
  targetCPUUtilizationPercentage: 10
```

## **Question 6**

Creating a filebeat yaml file (with the same version as the elasticsearch):

```
apiVersion: beat.k8s.elastic.co/v1beta1
kind: Beat
metadata:
  name: brigerpayfilebeat
spec:
  type: filebeat
  version: 7.6.2
  elasticsearchRef:
    name: bcdbridgerpayelasticsearchcd
  config:
    filebeat.inputs:
    - type: container
      paths:
      - /var/log/containers/*.log
  daemonSet:
    podTemplate:
      spec:
        dnsPolicy: ClusterFirstWithHostNet
        hostNetwork: true
        securityContext:
          runAsUser: 0
        containers:
        - name: filebeat
          volumeMounts:
          - name: varlogcontainers
            mountPath: /var/log/containers
          - name: varlogpods
            mountPath: /var/log/pods
          - name: varlibdockercontainers
            mountPath: /var/lib/docker/containers
        volumes:
        - name: varlogcontainers
          hostPath:
            path: /var/log/containers
        - name: varlogpods
          hostPath:
            path: /var/log/pods
        - name: varlibdockercontainers
          hostPath:
            path: /var/lib/docker/containers
```

p.c.

![the output:](https://mail.google.com/mail/u/0?ui=2&ik=fb202b4c3e&attid=0.1&permmsgid=msg-a:r7385239369018795686&th=18180f92acd55f93&view=fimg&fur=ip&sz=s0-l75-ft&attbid=ANGjdJ_YHxxssHIIjKdU4YDWcxky7MFc0kREKy-HaTj2Vb3ZouOEdb3BsKYRdex1Dwgifz9cc8ZhRrB5KX4thYJkNh49M4Vk8PgT6cgWxifXYARScbsb084-ZrFoxsU&disp=emb&realattid=ii_l4mon1kh0)

![the logs](https://mail.google.com/mail/u/0?ui=2&ik=fb202b4c3e&attid=0.4&permmsgid=msg-a:r1283313169053177535&th=181810e01dd72c95&view=fimg&fur=ip&sz=s0-l75-ft&attbid=ANGjdJ9DxwvQ9kNdXK5bm0rgcm4ZhwT9BBhWflfmSsrYdhkhhS3QpVuNKSo_gwEOYpx0xM7_ZFMRfC6PdneVe_RyyrVEFXLsqH4tBFGZsk48Xaoql9uR_2IAmpFr1n0&disp=emb&realattid=ii_l4mpehw03)

![](https://mail.google.com/mail/u/0?ui=2&ik=fb202b4c3e&attid=0.5&permmsgid=msg-a:r1283313169053177535&th=181810e01dd72c95&view=fimg&fur=ip&sz=s0-l75-ft&attbid=ANGjdJ8wBfWytNH4Y1x1meszCigX5kC__DtzGQvubF-BBjqPc7wga6zRED374fdGtYQn0lgFQCCQNuNppYg3gRuTw4FQoyB3kQFu6BMXwFZ9Ymq0Hdf1qj5jegtt3HA&disp=emb&realattid=ii_l4mpg6ze5)


## **Question 7**
Writing the small app:
```
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# initializations
app = Flask(__name__)


# routes
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM bridgerpaytable')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', bridgerpaytable = data)


# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)

```
### 1
This is my mysql table:
```
	CREATE TABLE `bridgerpaytable` (
	  `id` int(11) NOT NULL,
	  `current_datetime` TIMESTAMP NOT NULL,
	  `email` varchar(50) NOT NULL,
	  `comment` varchar(255) NOT NULL
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	ALTER TABLE `bridgerpaytable`
	  ADD PRIMARY KEY (`id`);

	ALTER TABLE `bridgerpaytable`
	  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
```
### 2 
Connection to the bridgerpaytable table and Writing the post and delete function:
```
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# initializations
app = Flask(__name__)

server_url = 'http://cdbridgerpayelasticsearch:9200'
service_name = 'BridgerpayFlask'
environment = 'dev'

apm = ElasticAPM(app, server_url=server_url, service_name=service_name, environment=environment)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'CDcd1212121'
app.config['MYSQL_DB'] = 'bcdexedbbcd'
mysql = MySQL(app)

# settings
# app.secret_key = "mysecretkey"

# routes
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM bridgerpaytable')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', bridgerpaytable = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        current_datetime = request.form['current_datetime']
        email = request.form['email']
        comment = request.form['comment']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO bridgerpaytable (current_datetime, email,comment) VALUES (%s,%s,%s)", (current_datetime, email,comment))
        mysql.connection.commit()
        flash('Contact Added successfully')
        return redirect(url_for('Index'))

@app.route('/delete/<ind:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM bridgerpaytable WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))

# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)

```
### 3

First I installed this:
>	pip install elastic-apm[flask]
and then I put this in the python code:
```
server_url = 'https:// bcdbridgerpayelasticsearch:9200'
service_name = 'BridgerpayFlask'
environment = 'dev'
```
And this:
```
apm = ElasticAPM(app, server_url=server_url, service_name=service_name, environment=environment)

```
Thank you
