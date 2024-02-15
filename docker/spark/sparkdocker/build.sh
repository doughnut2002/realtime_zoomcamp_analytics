# -- Software Stack Version

SPARK_VERSION="3.3.1"
HADOOP_VERSION="3"
JUPYTERLAB_VERSION="3.6.1"

# -- Building the Images

docker build \
  -f ./docker/spark/sparkdocker/cluster-base.Dockerfile \
  -t cluster-base .

docker build \
  --build-arg spark_version="${SPARK_VERSION}" \
  --build-arg hadoop_version="${HADOOP_VERSION}" \
  -f ./docker/spark/sparkdocker/spark-base.Dockerfile \
  -t spark-base .

docker build \
  -f ./docker/spark/sparkdocker/spark-master.Dockerfile \
  -t spark-master .

docker build \
  -f ./docker/spark/sparkdocker/spark-worker.Dockerfile \
  -t spark-worker .

docker build \
  --build-arg spark_version="${SPARK_VERSION}" \
  --build-arg jupyterlab_version="${JUPYTERLAB_VERSION}" \
  -f ./docker/spark/sparkdocker/jupyterlab.Dockerfile \
  -t jupyterlab .