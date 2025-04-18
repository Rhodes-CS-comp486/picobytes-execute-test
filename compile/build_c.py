import os, logging

logger = logging.getLogger(__name__)

def build(jobdir):
    logger.info("Building...")
    try:
        origin = os.path.dirname(os.path.realpath(__file__))
        tempCFile = os.path.join(jobdir, "tempC.c")
        tempTestFile = os.path.join(jobdir, "tempTest.c")
        finalCFile = os.path.join(jobdir, "final_c.c")

        logger.info(f"Temp C file: {tempCFile}, Temp test file: {tempTestFile}, Final C file: {finalCFile}")
        c_code = [];
        with open(tempCFile, "r") as file:
            lines = file.readlines()
            for line in lines:
                c_code.append(line.strip())
        logger.info("Read code")

        test_code = [];
        with open(tempTestFile, "r") as file:
            lines = file.readlines()
            for line in lines:
                test_code.append(line.strip())
        logger.info("Read test code")
        final_c_code = f"""
    #include <stdio.h>
    int run_success = 0;
    #define assert(condition) if (condition) {{printf("ASSERT PASSED!\\n");}} else {{printf("ASSERT FAILED: %s\\n", #condition);run_success = 1;}}

    {"\n".join(c_code)}
    int main(){{
    {"\n".join(test_code)}
    return run_success;
    }}"""

        with open(finalCFile, "w") as file:
            file.write(final_c_code)
            logger.info("Built and written to " + finalCFile)
        return 0
    except Exception as e:
        logger.error(e)
        print(e)
        return 1

