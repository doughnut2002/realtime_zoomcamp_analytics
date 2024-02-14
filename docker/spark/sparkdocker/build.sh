# -- Software Stack Version

SPARK_VERSION="3.3.1"
HADOOP_VERSION="3"
JUPYTERLAB_VERSION="3.6.1"

# -- Building the Images

docker build \
  -f ../docker/spark/cluster-base.Dockerfile \
  -t cluster-base .

docker build \
  --build-arg spark_version="${SPARK_VERSION}" \
  --build-arg hadoop_version="${HADOOP_VERSION}" \
  -f ../docker/spark/spark-base.Dockerfile \
  -t spark-base .

docker build \
  -f ../docker/spark/spark-master.Dockerfile \
  -t spark-master .

docker build \
  -f ../docker/spark/spark-worker.Dockerfile \
  -t spark-worker .

docker build \
  --build-arg spark_version="${SPARK_VERSION}" \
  --build-arg jupyterlab_version="${JUPYTERLAB_VERSION}" \
  -f ../docker/spark/jupyterlab.Dockerfile \
  -t jupyterlab .