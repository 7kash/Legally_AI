#!/bin/bash
echo "Running database migration to add user_id to analyses table..."
docker compose exec -T api alembic upgrade head
echo "Migration complete!"
echo ""
echo "Restarting API to apply changes..."
docker compose restart api celery
echo "Done!"
