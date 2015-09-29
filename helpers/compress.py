from compressor.filters import CompilerFilter


class LessFilter(CompilerFilter):
    command = 'lessc {infile} {outfile}'
