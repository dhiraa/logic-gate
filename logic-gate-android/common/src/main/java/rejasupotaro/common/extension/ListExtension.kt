package rejasupotaro.common.extension

import java.util.*

fun <E> List<E>.sample() = this[Random().nextInt(this.lastIndex + 1)]

