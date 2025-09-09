.PHONY: setup start clean

setup:
	python -m venv venv
	@echo "Virtual environment created"
	./venv/bin/pip install -r requirements.txt

start:
	@echo "Activating virtual environment..."
	@echo "Run: source venv/bin/activate"

clean:
	rm -rf venv
	@echo "Virtual environment removed"
