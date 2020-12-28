#!/bin/bash
. $PWD/.env

GREEN='\033[1;32m'
NO_COLOR='\033[0m'

CORE_DIRECTORY_PATH=$PWD/core
WEB_DIRECTORY_PATH=$PWD/web
SCRIPT_PATH=$PWD/scripts

function print_color_text() {
    TITLE=$1

    echo -e "\n${GREEN}>>>> ${TITLE} ${NO_COLOR}\n"
}

function build_docker_image() {
    print_color_text "Build docker image start"
    ${SCRIPT_PATH}/build.sh core
    ${SCRIPT_PATH}/build.sh web
    print_color_text "Build docker image done"
}

function run_docker_compose() {
    print_color_text "Run docker compose start"
    ${SCRIPT_PATH}/run.sh all
    print_color_text "Run docker compose done"
}

function migrate_database() {
    print_color_text "Migrate database start"
    ${SCRIPT_PATH}/migrate.sh
    print_color_text "Migrate database done"
}

function insert_base_data() {
    print_color_text "Insert base data start"
    ${SCRIPT_PATH}/insert_base_data.sh
    print_color_text "Insert base data done"
}

function build_frontend_js() {
    print_color_text "Build frontend js start"
    ${SCRIPT_PATH}/build.sh frontend
    print_color_text "Build frontend js done"
}

build_docker_image

run_docker_compose

# migrate_database

# insert_base_data

# build_frontend_js

# run_docker_compose