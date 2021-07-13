from shared.BaseUnitTest import BaseUnitTest
from shared.CustomProfiler import stop_profiler, start_profiler
from shared.FileUtilities import getfemale_babies_file_name, create_output_file, get_babies_csv_file_name, \
    get_current_path
from streams.FileStream import FileStream
from streams.operations.operators import item


class TestFileStream(BaseUnitTest):
    def test_as_csv_operator(self):
        filename = get_current_path() + '\\resources\\babynames.csv'
        #
        # csv = "babynames.csv"
        # outputfile = "results.csv"
        full_path_of_input_csv = filename
        full_path_of_output_csv = create_output_file("baby_names_starts_with_a.csv")
        (FileStream.createFromCsv(full_path_of_input_csv)
         .filter(item['Female name'].startswith("A"))
         .map(item['Female name'])
         .peek(item.print)
         .asCSV(full_path_of_output_csv))
        self.assertFileExists(full_path_of_output_csv)
        self.assertFileContentContains(full_path_of_output_csv, "Amelia")

    def test_as_file(self):
        filename = getfemale_babies_file_name()
        outputFile = create_output_file("baby_names_starts_with_a.txt")
        start_profiler()
        (FileStream.createFromText(filename)
         .filter(lambda value: value.startswith("A"))
         .peek(lambda val: print(val))
         .asTextFile(outputFile))
        stop_profiler()
        self.assertFileExists(outputFile)
        self.assertFileContentContains(outputFile, "Amelia")

    # def test_as_file_profiler(self):
    #
    #     filename = getfemale_babies_file_name()
    #     outputFile = create_output_file("baby_names_starts_with_a.txt")
    #     #3198 function calls in 0.003 seconds
    #     start_profiler()
    #     (FileStream.createFromText(filename)
    #                 .filter(lambda value:value.startswith("A"))
    #                 .asTextFile(outputFile))
    #     stop_profiler()
    #     self.assertFileExists(outputFile)
    #     self.assertFileContentContains(outputFile,"Amelia")

    def test_as_csv(self):
        filename = get_babies_csv_file_name()
        outputFile = create_output_file("baby_names_starts_with_a.csv")
        start_profiler()
        (FileStream.createFromCsv(filename)
         .filter(lambda value: value['Female name'].startswith("A"))
         .peek(lambda val: print(val))
         .asCSV(outputFile))
        stop_profiler()
        self.assertFileExists(outputFile)
        self.assertFileContentContains(outputFile, "Amelia")

    def test_as_csv_example_2(self):
        filename = get_babies_csv_file_name()
        outputFile = create_output_file("baby_names_starts_with_a_single.csv")
        start_profiler()
        (FileStream.createFromCsv(filename)
         .filter(lambda value: value['Female name'].startswith("A"))
         .map(lambda value: value['Female name'])
         .peek(lambda val: print(val))
         .asCSV(outputFile))
        stop_profiler()
        self.assertFileExists(outputFile)
        self.assertFileContentContains(outputFile, "Amelia")
