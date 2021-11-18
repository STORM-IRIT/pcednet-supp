#!/bin/sh

# USAGE
# deploy.sh DEPLOYMENT_MODE DEPLOY_PATH WIPE_DEPLOY_FOLDER
# with:
#  DEPLOYMENT_MODE: server or local
#  DEPLOY_PATH: absolute or relative path to deployment directory
#  WIPE_DEPLOY_FOLDER: true or false

# OPTIONS
DEPLOYMENT_MODE=$1
DEPLOY_PATH=$2
WIPE_DEPLOY_FOLDER=$3

if [ "${WIPE_DEPLOY_FOLDER}" = true ] ; then
  echo "[SCRIPT STEP] Preparing local deployment"
  rm -rf ${DEPLOY_PATH}
  mkdir -pv ${DEPLOY_PATH}
fi

echo "[SCRIPT STEP] Copying assets"
cp -rv assets ${DEPLOY_PATH}
cp -rv images ${DEPLOY_PATH}
if [ "${DEPLOYMENT_MODE}" = "server" ] ; then
  cp -rv 3dmodels ${DEPLOY_PATH}
fi

echo "[SCRIPT STEP] Use PLY2JS 3d models js scripts"
python3 deploy3dmodels.py ${DEPLOY_PATH} ${DEPLOYMENT_MODE}

echo "[SCRIPT STEP] Generate dataset js scripts"
python3 deployStatistics.py ${DEPLOY_PATH}

echo "[SCRIPT STEP] Generate html pages"
python3 deployHtml.py ${DEPLOY_PATH}  ${DEPLOYMENT_MODE}
