#include <CUnit/Basic.h>
#include "script.h"

/* Test function */
static int test1() {
    return 1;
}

/* Test cases */
void test_success(void) {
    CU_ASSERT(test1() == 1);
    CU_ASSERT_EQUAL(test1(), 1);
}

void test_failure(void) {
    CU_ASSERT(test1() > 1);  // This should fail
    CU_ASSERT_EQUAL(run(), 1);
}

/* Optional: Suite initialization and cleanup functions */
int init_suite(void) {
    return 0;  // Return 0 on success, non-zero on error
}

int clean_suite(void) {
    return 0;  // Return 0 on success, non-zero on error
}

int main(int argc, char **argv) {
    /* Initialize CUnit test registry */
    if (CUE_SUCCESS != CU_initialize_registry()) {
        return CU_get_error();
    }

    /* Create test suite */
    CU_pSuite suite = CU_add_suite("test_suite1", init_suite, clean_suite);
    if (NULL == suite) {
        CU_cleanup_registry();
        return CU_get_error();
    }

    /* Add tests to suite */
    if ((NULL == CU_add_test(suite, "test of test1() success", test_success)) ||
        (NULL == CU_add_test(suite, "test of test1() failure", test_failure))) {
        CU_cleanup_registry();
        return CU_get_error();
    }

    /* Run tests using Basic interface */
    CU_basic_set_mode(CU_BRM_VERBOSE);
    CU_basic_run_tests();
    
    /* Get number of failures */
    unsigned int num_failures = CU_get_number_of_failures();
    
    /* Cleanup registry */
    CU_cleanup_registry();

    return num_failures;
}
