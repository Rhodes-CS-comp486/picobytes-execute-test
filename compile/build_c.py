import os
def build():
    try:
        origin = os.path.dirname(os.path.realpath(__file__))
        tempCFile = os.path.join(origin, "tempC.c")
        tempTestFile = os.path.join(origin, "tempTest.c")
        finalCFile = os.path.join(origin, "final_c.c")
        c_code = [];
        with open(tempCFile, "r") as file:
            lines = file.readlines()
            for line in lines:
                c_code.append(line.strip())

        test_code = [];
        with open(tempTestFile, "r") as file:
            lines = file.readlines()
            for line in lines:
                test_code.append(line.strip())
        print(test_code)
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
        return 0
    except Exception as e:
        print(e)
        return 1

