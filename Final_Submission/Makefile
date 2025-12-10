# Footy Liveliness - Root Makefile
# Quick access to web application commands

.PHONY: help install start stop demo status clean scrape update test validate open logs

WEB_APP_DIR = 4_Web_Application/footy-liveliness-web

help:
	@echo "╔════════════════════════════════════════════════════════════════╗"
	@echo "║         Footy Liveliness - Quick Start Commands               ║"
	@echo "╚════════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "Available commands:"
	@echo ""
	@echo "  make install    - Install all dependencies"
	@echo "  make start      - Start the application"
	@echo "  make stop       - Stop the application"
	@echo "  make demo       - Full demo (install + scrape + start)"
	@echo "  make update     - Re-scrape data and restart application"
	@echo "  make status     - Check application status"
	@echo "  make clean      - Clean up temporary files"
	@echo ""
	@echo "Quick Start:"
	@echo "  make install && make start"
	@echo ""
	@echo "Or for full demo with live data:"
	@echo "  make demo"
	@echo ""
	@echo "For more commands, see:"
	@echo "  cd $(WEB_APP_DIR) && make help"
	@echo ""

install:
	@cd $(WEB_APP_DIR) && make install

start:
	@cd $(WEB_APP_DIR) && make start

stop:
	@cd $(WEB_APP_DIR) && make stop

demo:
	@cd $(WEB_APP_DIR) && make demo

status:
	@cd $(WEB_APP_DIR) && make status

clean:
	@cd $(WEB_APP_DIR) && make clean

scrape:
	@cd $(WEB_APP_DIR) && make scrape

update:
	@cd $(WEB_APP_DIR) && make update

test:
	@cd $(WEB_APP_DIR) && make test

validate:
	@cd $(WEB_APP_DIR) && make validate

open:
	@cd $(WEB_APP_DIR) && make open

logs:
	@cd $(WEB_APP_DIR) && make logs
