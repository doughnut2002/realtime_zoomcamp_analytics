docker-compose -f ./docker/mage/docker-compose.yml up -d
docker-compose -f ./docker/postgres/docker-compose.yml up -d


sudo cp ./Batch_Pipeline/Data_Exporter/* ./docker/mage/Shekhar-IQ/data_exporters/

sudo cp ./Batch_Pipeline/Data_Loader/* ./docker/mage/Shekhar-IQ/data_loaders/

sudo mkdir ./docker/mage/Shekhar-IQ/pipelines/kind_voice

sudo cp ./Batch_Pipeline/metadata.yaml ./docker/mage/Shekhar-IQ/pipelines/kind_voice/
sudo cp ./Batch_Pipeline/__init__.py ./docker/mage/Shekhar-IQ/pipelines/kind_voice/
sudo cp ./Batch_Pipeline/triggers.yaml ./docker/mage/Shekhar-IQ/pipelines/kind_voice/


sudo cp ./Batch_Pipeline/io_config.yaml ./docker/mage/Shekhar-IQ/


curl -X POST http://localhost:6789/api/pipeline_schedules/1/pipeline_runs/8bd706fac5684ff08678e3bc643903c1
