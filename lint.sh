#!/bin/bash
poetry run autoflake --in-place --recursive --remove-all-unused-imports --remove-duplicate-keys --remove-unused-variables graphene_djmoney tests test_app
poetry run flake8 graphene_djmoney tests test_app
poetry run bandit -r graphene_djmoney/
poetry run ssort graphene_djmoney tests test_app
poetry run isort graphene_djmoney tests test_app
poetry run black .
