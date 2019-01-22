#!/bin/bash

export DILATED_CNN_NER_ROOT=`pwd`
export DATA_DIR=/Users/nhnent/dev/data/pos_sejong800k/conll
export CUDA_VISIBLE_DEVICES=-1

conf=$1
if [ ! -e $conf ]; then
    echo "No config file specified; Exiting."
    exit 1
fi
source $conf

additional_args=${@:2}

if [[ "$2" == "test" ]]; then
    dev_dir=$test_dir
    additional_args=${@:3}
fi

# star escaping
dev_fixed=`echo "$dev_dir" | sed 's/\*/\\\*/'`

cmd="$DILATED_CNN_NER_ROOT/bin/train-cnn.sh \
$conf \
--evaluate_only \
--train_eval \
--load_dir $model_dir \
--dev_dir $dev_fixed \
$additional_args"

echo ${cmd}
eval ${cmd}
