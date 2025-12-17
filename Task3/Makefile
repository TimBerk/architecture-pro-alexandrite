start:
	minikube start --addons=ingress
	kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.3/cert-manager.yaml
jaeger:
	kubectl create namespace observability
	kubectl create -f https://github.com/jaegertracing/jaeger-operator/releases/download/v1.51.0/jaeger-operator.yaml -n observability
	kubectl apply -f k8s/jaeger-instance.yaml
	kubectl port-forward svc/simplest-query 16686:16686
service:
	minikube image build -t service-a:latest services/service-a/
	minikube image build -t service-b:latest services/service-b/
	kubectl apply -f k8s/services.yaml