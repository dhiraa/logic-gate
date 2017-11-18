package rejasupotaro.logicgate

import android.content.res.AssetManager
import org.tensorflow.contrib.android.TensorFlowInferenceInterface

class LogicGate(assets: AssetManager, private val logger: (String) -> Unit = {}) {
    private val inferenceInterface = TensorFlowInferenceInterface(assets, "xor_keras.pb")
    private val inputName = "dense_1_input_1"
    private val outputName = "output_0"

    init {
        for (op in inferenceInterface.graph().operations()) {
            logger("name: ${op.name()}, type: ${op.type()}, numOutputs: ${op.numOutputs()}")
        }
    }

    fun xor(x1: Int, x2: Int): Int {
        val input = floatArrayOf(x1.toFloat(), x2.toFloat())
        inferenceInterface.feed(inputName, input, 1, 2)
        inferenceInterface.run(arrayOf(outputName))

        val output = FloatArray(1)
        inferenceInterface.fetch(outputName, output)

        logger("input: [$x1, $x2] => output (probability): ${output[0]}")

        return if (output[0] < 0.5) 0 else 1
    }
}

