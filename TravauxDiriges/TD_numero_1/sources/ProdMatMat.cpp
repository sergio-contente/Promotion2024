#include <algorithm>
#include <cassert>
#include <iostream>
#include <thread>
#if defined(_OPENMP)
#include <omp.h>
#endif
#include "ProdMatMat.hpp"
// #ifdef _OPENMP
//     omp_set_num_threads(8); // Remplacez 8 par le nombre souhaité de threads
//   #endif
namespace {
void prodSubBlocks(int iRowBlkA, int iColBlkB, int iColBlkA, int szBlock,
                   const Matrix& A, const Matrix& B, Matrix& C) {
  
  #pragma omp parallel for collapse(3)
  for (int j = iColBlkB; j < std::min(B.nbCols, iColBlkB + szBlock); j++)
  for (int k = iColBlkA; k < std::min(A.nbCols, iColBlkA + szBlock); k++)
  for (int i = iRowBlkA; i < std::min(A.nbRows, iRowBlkA + szBlock); ++i)
        C(i, j) += A(i, k) * B(k, j);
}
const int szBlock = 32;
}  // namespace

Matrix operator*(const Matrix& A, const Matrix& B) {
  Matrix C(A.nbRows, B.nbCols, 0.0);
  prodSubBlocks(0, 0, 0, std::max({A.nbRows, B.nbCols, A.nbCols}), A, B, C);
  return C;
}
