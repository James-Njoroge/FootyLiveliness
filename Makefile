.PHONY: install test clean

install:
	@echo "📦 Installing Python dependencies..."
	pip install -r Final_Submission/4_Web_Application/footy-liveliness-web/requirements.txt
	@echo "✅ Dependencies installed successfully!"

test:
	@echo "🧪 Running basic checks..."
	python -c "import flask; import pandas; import numpy; import sklearn; print('✅ All core dependencies imported successfully!')"
	@echo "✅ Basic checks passed!"

clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cleanup complete!"
