#!/bin/bash
echo "Setando as variaveis de ambiente"
echo $(grep -v '^#' .env | xargs)
export $(grep -v '^#' .env | xargs -d '\n')
