from pathlib import Path
from unittest import TestCase

from shared.BaseUnitTest import BaseUnitTest
from shared.CustomProfiler import stop_profiler, start_profiler
from shared.FileUtilities import getfemale_babies_file_name, create_output_file
from streams.FileStream import FileStream


class TestFileStream(BaseUnitTest):
    def test_as_file(self):

        filename = getfemale_babies_file_name()
        outputFile = create_output_file("baby_names_starts_with_a.txt")
        start_profiler()
        (FileStream.create(filename)
                    .filter(lambda value:value.startswith("A"))
                    .peek(lambda val:print(val))
                    .asFile(outputFile))
        stop_profiler()
        self.assertFileExists(outputFile)
        self.assertFileContentContains(outputFile,"Amelia")

    def test_as_file_profiler(self):

        filename = getfemale_babies_file_name()
        outputFile = create_output_file("baby_names_starts_with_a.txt")
        #3198 function calls in 0.003 seconds
        start_profiler()
        (FileStream.create(filename)
                    .filter(lambda value:value.startswith("A"))
                    .asFile(outputFile))
        stop_profiler()
        self.assertFileExists(outputFile)
        self.assertFileContentContains(outputFile,"Amelia")
