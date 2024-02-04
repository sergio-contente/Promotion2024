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

  int jEnd = std::min(B.nbCols, iColBlkB + szBlock);
  int kEnd = std::min(A.nbCols, iColBlkA + szBlock);
  int iEnd = std::min(A.nbRows, iRowBlkA + szBlock);
  
  #pragma omp parallel for collapse (2)
  for (int j = iColBlkB; j < jEnd; j++)
  for (int k = iColBlkA; k < kEnd; k++)
  for (int i = iRowBlkA; i < iEnd; ++i)
        C(i, j) += A(i, k) * B(k, j);
}
const int szBlock = 1024;
}  // namespace

Matrix operator*(const Matrix& A, const Matrix& B) {
  Matrix C(A.nbRows, B.nbCols, 0.0);
  //prodSubBlocks(0, 0, 0, std::max({A.nbRows, B.nbCols, A.nbCols}), A, B, C);
   for (int iRowBlkA = 0; iRowBlkA < A.nbRows; iRowBlkA += szBlock) {
    for (int iColBlkB = 0; iColBlkB < B.nbCols; iColBlkB += szBlock) {
      for (int iColBlkA = 0; iColBlkA < A.nbCols; iColBlkA += szBlock) {
        prodSubBlocks(iRowBlkA, iColBlkB, iColBlkA, szBlock, A, B, C);
      }
    }
  }
  return C;
}
