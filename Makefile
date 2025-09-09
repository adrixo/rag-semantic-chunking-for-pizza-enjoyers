.PHONY: setup start clean

setup:
	python -m venv venv
	@echo "Virtual environment created"
	./venv/bin/pip install -r requirements.txt
	cd supabase-docker 
	docker compose pull
	docker compose up -d
	@echo "following steps at https://supabase.com/docs/guides/self-hosting/docker"
	@echo "ensure the docker socket is available (see guide)"

start:
	@echo "Activating virtual environment..."
	@echo "Run: source venv/bin/activate"

clean:
	rm -rf venv
	@echo "Virtual environment removed"
