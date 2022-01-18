__author__ = "David Laehnemann, Victoria Sack"
__copyright__ = "Copyright 2018, David Laehnemann, Victoria Sack"
__email__ = "david.laehnemann@hhu.de"
__license__ = "MIT"


import os
import tempfile
from snakemake.shell import shell

params_sort = snakemake.params.get("sort", "")
params_fastq = snakemake.params.get("fastq", "")
log = snakemake.log_fmt_shell(stdout=True, stderr=True)

prefix = os.path.splitext(snakemake.output[0])[0]

# Samtools takes additional threads through its option -@
# One thread is used bu Samtools sort
# One thread is used by Samtools fastq
# So snakemake.threads has to take them into account
# before allowing additional threads through samtools sort -@
threads = "" if snakemake.threads <= 2 else " -@ {} ".format(snakemake.threads - 2)

with tempfile.NamedTemporaryFile() as tmpfile:
    shell(
        "(samtools sort -n "
        " {threads} "
        " -T {tmpfile.name} "
        " {params_sort} "
        " {snakemake.input[0]} | "
        "samtools fastq "
        " {params_fastq} "
        " -1 {snakemake.output[0]} "
        " -2 {snakemake.output[1]} "
        " -0 /dev/null "
        " -s /dev/null "
        " -F 0x900 "
        " - "
        ") {log}"
    )