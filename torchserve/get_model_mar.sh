torch-model-archiver --model-name toxic_classifier \
                     --version 1.0 \
                     --model-file model.py \
                     --serialized-file saved_weights.pt \
                     --handler handler.py \

rm models/toxic_classifier.mar
mv toxic_classifier.mar models