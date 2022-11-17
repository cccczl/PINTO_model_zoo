### tf-nightly-2.2.0.dev20200418

import tensorflow as tf
from tensorflow.python import ops
import shutil

def get_graph_def_from_file(graph_filepath):
    tf.compat.v1.reset_default_graph()
    with ops.Graph().as_default():
        with tf.compat.v1.gfile.GFile(graph_filepath, 'rb') as f:
            graph_def = tf.compat.v1.GraphDef()
            graph_def.ParseFromString(f.read())
            return graph_def

def convert_graph_def_to_saved_model(export_dir, graph_filepath, input_name, outputs):
    graph_def = get_graph_def_from_file(graph_filepath)
    with tf.compat.v1.Session(graph=tf.Graph()) as session:
        tf.import_graph_def(graph_def, name='')
        tf.compat.v1.saved_model.simple_save(
            session,
            export_dir,
            inputs={
                input_name: session.graph.get_tensor_by_name(f'{node.name}:0')
                for node in graph_def.node
                if node.op == 'Placeholder'
            },
            outputs={
                t.rstrip(":0"): session.graph.get_tensor_by_name(t)
                for t in outputs
            },
        )

        print('Optimized graph converted to SavedModel!')

shutil.rmtree('saved_model_detnet', ignore_errors=True)
convert_graph_def_to_saved_model('saved_model_detnet', 'freeze_graph_detnet.pb', 'input', ['prior_based_hand/strided_slice_6:0', 'prior_based_hand/strided_slice_7:0'])

shutil.rmtree('saved_model_iknet', ignore_errors=True)
convert_graph_def_to_saved_model('saved_model_iknet', 'freeze_graph_iknet.pb', 'input', ['network/Select:0'])