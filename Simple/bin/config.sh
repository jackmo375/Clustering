wk='/home/jack/Local/Learning/DataAnalysis/Clustering/Simple/'
source=${wk}'src/'
data=${wk}'data/'
media=${wk}'media/'

# python variables
pyenv='clusterENV'

check_py_enviroment() {
	env=$(which python)
	if [[ $env != *${pyenv}* ]]; then
		echo 'current python enviroment is: '$env
		echo 'ERROR: please load the correct python enviroment and try again.'
		exit 1
	fi
}
