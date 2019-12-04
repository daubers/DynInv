

run_local_consul:
	/home/matt/Apps/consul agent -ui -bind 172.19.0.1 -dev -join=172.19.0.2 -config-dir health_checks -enable-local-script-checks --server-port 8900 --http-port 9000