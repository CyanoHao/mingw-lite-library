target("openblas/lapacke-example_user")
  on_config(pkgconf("openblas"))
  add_files("lapacke-example_user.c")
  add_tests("default", {
    pass_outputs =
      "\n" ..
      " Entry Matrix A\n" ..
      "   6.80  -6.05  -0.45   8.32  -9.67\n" ..
      "  -2.11  -3.30   2.58   2.71  -5.14\n" ..
      "   5.66   5.36  -2.70   4.35  -7.26\n" ..
      "   5.97  -4.44   0.27  -7.17   6.08\n" ..
      "   8.23   1.08   9.04   2.14  -6.87\n" ..
      "\n" ..
      " Right Rand Side\n" ..
      "   4.02  -1.56   9.81\n" ..
      "   6.19   4.00  -4.09\n" ..
      "  -8.22  -8.67  -4.57\n" ..
      "  -7.57   1.75  -8.61\n" ..
      "  -3.03   2.86   8.99\n" ..
      "\n" ..
      "LAPACKE_dgecon Example Program Results\n" ..
      "LAPACKE_dgecon completed SUCCESSFULLY...\n" ..
      "LAPACKE_dlange / One-norm of A = 35.020000\n" ..
      "LAPACKE_dgecon / RCOND of A    = 0.035419\n",
    plain = true})
