import tensorflow as tf
import os
import shutil
from tensorflow.python.saved_model import tag_constants
from tensorflow.python.tools import freeze_graph
from tensorflow.python import ops
#from tensorflow.tools.graph_transforms import TransformGraph

def freeze_model(saved_model_dir, output_node_names, output_filename):
  output_graph_filename = os.path.join(saved_model_dir, output_filename)
  initializer_nodes = ''
  freeze_graph.freeze_graph(
      input_saved_model_dir=saved_model_dir,
      output_graph=output_graph_filename,
      saved_model_tags = tag_constants.SERVING,
      output_node_names=output_node_names,
      initializer_nodes=initializer_nodes,
      input_graph=None,
      input_saver=False,
      input_binary=False,
      input_checkpoint=None,
      restore_op_name=None,
      filename_tensor_name=None,
      clear_devices=True,
      input_meta_graph=False,
  )

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
            for node in graph_def.node if node.op == 'Placeholder'
        },
        outputs={
            t.rstrip(":0"): session.graph.get_tensor_by_name(t)
            for t in outputs
        },
    )
    print('Optimized graph converted to SavedModel!')

tf.compat.v1.enable_eager_execution()

# Look up the name of the placeholder for the input node
graph_def=get_graph_def_from_file('./model-mobilenet_v1_101_225.pb')
input_name=""
for node in graph_def.node:
    if node.op=='Placeholder':
        print("##### model-mobilenet_v1_101_225 - Input Node Name #####", node.name) # this will be the input node
        input_name=node.name

# model-mobilenet_v1_101_225 output names
output_node_names = ['heatmap','offset_2','displacement_fwd_2','displacement_bwd_2']
outputs = ['heatmap:0','offset_2:0','displacement_fwd_2:0','displacement_bwd_2:0']

# convert this to a TF Serving compatible mode - model-mobilenet_v1_101_225
shutil.rmtree('./0', ignore_errors=True)
convert_graph_def_to_saved_model('./0', './model-mobilenet_v1_101_225.pb', input_name, outputs)



## Look up the name of the placeholder for the input node
#graph_def=get_graph_def_from_file('./model-mobilenet_v1_101_257.pb')
#input_name=""
#for node in graph_def.node:
#    if node.op=='Placeholder':
#        print("##### model-mobilenet_v1_101_257 - Input Node Name #####", node.name) # this will be the input node
#        input_name=node.name

## model-mobilenet_v1_101_257 output names
#output_node_names = ['heatmap','offset_2','displacement_fwd_2','displacement_bwd_2']
#outputs = ['heatmap:0','offset_2:0','displacement_fwd_2:0','displacement_bwd_2:0']

## convert this to a TF Serving compatible mode - model-mobilenet_v1_101_257
#shutil.rmtree('./0', ignore_errors=True)
#convert_graph_def_to_saved_model('./0', './model-mobilenet_v1_101_257.pb', input_name, outputs)



## Look up the name of the placeholder for the input node
#graph_def=get_graph_def_from_file('./model-mobilenet_v1_101_321.pb')
#input_name=""
#for node in graph_def.node:
#    if node.op=='Placeholder':
#        print("##### model-mobilenet_v1_101_321 - Input Node Name #####", node.name) # this will be the input node
#        input_name=node.name

## model-mobilenet_v1_101_321 output names
#output_node_names = ['heatmap','offset_2','displacement_fwd_2','displacement_bwd_2']
#outputs = ['heatmap:0','offset_2:0','displacement_fwd_2:0','displacement_bwd_2:0']

## convert this to a TF Serving compatible mode - model-mobilenet_v1_101_321
#shutil.rmtree('./0', ignore_errors=True)
#convert_graph_def_to_saved_model('./0', './model-mobilenet_v1_101_321.pb', input_name, outputs)



## Look up the name of the placeholder for the input node
#graph_def=get_graph_def_from_file('./model-mobilenet_v1_101_385.pb')
#input_name=""
#for node in graph_def.node:
#    if node.op=='Placeholder':
#        print("##### model-mobilenet_v1_101_385 - Input Node Name #####", node.name) # this will be the input node
#        input_name=node.name

## model-mobilenet_v1_101_385 output names
#output_node_names = ['heatmap','offset_2','displacement_fwd_2','displacement_bwd_2']
#outputs = ['heatmap:0','offset_2:0','displacement_fwd_2:0','displacement_bwd_2:0']

## convert this to a TF Serving compatible mode - model-mobilenet_v1_101_385
#shutil.rmtree('./0', ignore_errors=True)
#convert_graph_def_to_saved_model('./0', './model-mobilenet_v1_101_385.pb', input_name, outputs)



## Look up the name of the placeholder for the input node
#graph_def=get_graph_def_from_file('./model-mobilenet_v1_101_513.pb')
#input_name=""
#for node in graph_def.node:
#    if node.op=='Placeholder':
#        print("##### model-mobilenet_v1_101_513 - Input Node Name #####", node.name) # this will be the input node
#        input_name=node.name

## model-mobilenet_v1_101_513 output names
#output_node_names = ['heatmap','offset_2','displacement_fwd_2','displacement_bwd_2']
#outputs = ['heatmap:0','offset_2:0','displacement_fwd_2:0','displacement_bwd_2:0']

## convert this to a TF Serving compatible mode - model-mobilenet_v1_101_513
#shutil.rmtree('./0', ignore_errors=True)
#convert_graph_def_to_saved_model('./0', './model-mobilenet_v1_101_513.pb', input_name, outputs)
