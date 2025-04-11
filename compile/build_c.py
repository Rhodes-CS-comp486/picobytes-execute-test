import os, logging, re

logger = logging.getLogger(__name__)

def strip_junk(code):
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    code = re.sub(r'//.*', '', code)
    code = re.sub(r'"(?:\\.|[^"\\])*"', '', code)
    code = re.sub(r"'(?:\\.|[^'\\])*'", '', code)
    return code

def extract_function_calls(code):
    code = strip_junk(code)
    candidates = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', code)

    blacklist = {
        'if', 'for', 'while', 'switch', 'return', 'sizeof',
        'typedef', 'struct', 'union', 'do', 'case', 'break', 'continue',
        'else', 'goto', 'static', 'const', 'volatile', 'register',
        'inline', 'restrict', 'default', 'enum', 'extern',
        'int', 'float', 'double', 'char', 'void', 'long', 'short', 'unsigned', 'signed',
        '__attribute__', '__builtin_va_arg', '__builtin_offsetof'
    }

    return sorted(set(name for name in candidates if name not in blacklist))

def build(blacklist=None, whitelist=None):
    logger.info("Building...")
    try:
        origin = os.path.dirname(os.path.realpath(__file__))
        tempCFile = os.path.join(origin, "tempC.c")
        tempTestFile = os.path.join(origin, "tempTest.c")
        finalCFile = os.path.join(origin, "final_c.c")

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
        header_code = f"""
    int run_success = 0;
    #define assert(condition) if (condition) {{printf("ASSERT PASSED!\\n");}} else {{printf("ASSERT FAILED: %s\\n", #condition);run_success = 1;}}
        """

        filter_c_code = ""
        if blacklist is not None:
            pragma_poison = f"#pragma GCC poison " + " ".join(blacklist) + "\n"
            filter_c_code = pragma_poison



        if whitelist is not None:
            functions = extract_function_calls("\n".join(c_code))
            if any(func not in whitelist for func in functions):
                logger.error("Use of functions that are not in the allowed list.")
                return 1


        body_code = f"""
        {"\n".join(c_code)}

        int main(){{
            {"\n".join(test_code)}
            return run_success;
        }}
            """
        final_c_code = header_code + filter_c_code + body_code

        with open(finalCFile, "w") as file:
            file.write(final_c_code)
            logger.info("Built and written to " + finalCFile)
        return 0
    except Exception as e:
        logger.error(e)
        print(e)
        return 1

