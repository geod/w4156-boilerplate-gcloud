#!/bin/bash
# deploy master to prod

curl \
--header "Content-Type: application/json" \
--data '{"build_parameters": {"DEPLOY_STAGING_TO_PRODUCTION": "true"}}' \
https://circleci.com/api/v1.1/project/github/js4785/gennyc/tree/master?circle-token=de41c8ea8be457c846abafb0ad1ebd78dec93fdf
