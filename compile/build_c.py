def build():
    try:
        c_code = [];
        with open("tempC.c", "r") as file:
            lines = file.readlines()
            for line in lines:
                c_code.append(line.strip())

        test_code = [];
        with open("tempTest.c", "r") as file:
            lines = file.readlines()
            for line in lines:
                test_code.append(line.strip())

        final_c_code = f"""#include <assert.h>
    #include <stdio.h>
    {"\n".join(c_code)}
    int main(){{
    {"\n".join(test_code)}
    return 0;
    }}"""

        with open("final_c.c", "w") as file:
            file.write(final_c_code)
        return 0
    except Exception as e:
        print(e)
        return 1

