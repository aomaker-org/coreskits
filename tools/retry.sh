# 20250822 fekerr
# retry.sh: run with ". retry.sh" our "source retry.sh"
# so no shbang

SSH_PUB=/home/fekerr/.ssh/id_ed25519_24_20241126.pub
alias run='/home/fekerr/src/jules/aomaker02/runpy/run.py doit'

RETRY_CMD='/home/fekerr/src/jules/aomaker02/runpy/run.py doit'

echo ${PWD}, ${0}, ${@}: "Aliases and SSH_PUB loaded from retry.sh"

${RETRY_CMD} list
${RETRY_CMD} build_docker
