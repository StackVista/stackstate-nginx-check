import org.apache.commons.math3.stat.StatUtils

def freeMean = StatUtils.mean(freeStream.collect { it.point }.toArray() as double[])
def usedMean = StatUtils.mean(usedStream.collect { it.point }.toArray() as double[])

if(freeMean == 0 && usedMean == 0) return UNKNOWN;

def ratio = Math.abs(usedMean / (freeMean + usedMean))

if (ratio > criticalValue) return CRITICAL;
if (ratio > deviatingValue) return DEVIATING;

return CLEAR;