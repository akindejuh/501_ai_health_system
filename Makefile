## ── Monorepo commands ──────────────────────────

install:
	$(MAKE) -C backend install
	$(MAKE) -C frontend install

dev-backend:
	$(MAKE) -C backend dev

dev-frontend:
	$(MAKE) -C frontend dev

build:
	$(MAKE) -C backend build 2>/dev/null || true
	$(MAKE) -C frontend build

lint:
	$(MAKE) -C frontend lint

## ── Docker ─────────────────────────────────────

up:
	docker compose up --build

up-d:
	docker compose up --build -d

down:
	docker compose down
