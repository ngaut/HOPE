#include "gtest/gtest.h"

#include <assert.h>

#include <bitset>
#include <fstream>
#include <iostream>
#include <vector>
#include <algorithm>

#include "Tree_ArtDic.h"
#include "symbol_selector_factory.hpp"
#include "code_generator_factory.hpp"
#include "double_char_encoder.hpp"

namespace ARTDIC {

    namespace treetest {
        static const std::string kEmailFilePath = "../../../datasets/emails.txt";
        static const int kEmailTestSize = 10000;
        static std::vector<std::string> emails;


        class ARTDICTest : public ::testing::Test {
        public:
            static std::string getNextString(std::string str) {
                for (int i = int(str.size() - 1); i >= 0; i--) {
                    if (int(str[i]) != 127) {
                        char next_chr = str[i] + 1;
                        return str.substr(0, i) + std::string(1, next_chr);
                    }
                }
                assert(false);
                __builtin_unreachable();
            }

            static void getNextInterval(std::vector<std::string> sorted_intervals,
                                        int cur_idx, std::string cur_str,
                                        int& next_idx, std::string& next_str) {
                for (int i = cur_idx; i < sorted_intervals.size(); i++) {
                    if (sorted_intervals[i].compare(cur_str) > 0) {
                        next_idx = i - 1;
                        next_str = sorted_intervals[i-1];
                        return;
                    }
                }
                assert(false);
                __builtin_unreachable();
            }
        };

        TEST_F (ARTDICTest, emptyTest) {

        }

        TEST_F(ARTDICTest, pointLookupTest) {
            Tree *test = new Tree();
            std::vector<ope::SymbolCode> ls;
            // std::cout << emails.size() << std::endl;
            std::sort(emails.begin(), emails.end());

            for (int i = 0; i < emails.size(); i++) {
                ope::SymbolCode symbol_code = ope::SymbolCode();
                symbol_code.first = emails[i];
                symbol_code.second = ope::Code();
                symbol_code.second.code = i;
                ls.push_back(symbol_code);
            }

            test->build(ls);

            for (int i = 0; i < emails.size(); i++) {
                int prefix_len = -1;
                ope::Code result = test->lookup(emails[i].c_str(), emails[i].size(), prefix_len);
                ASSERT_TRUE(result.code == i);
            }
            delete test;
        }

        TEST_F(ARTDICTest, withinRangeLookupTest) {
            Tree *test = new Tree();
            std::vector<ope::SymbolCode> ls;
            std::cout << emails.size() << std::endl;
            std::sort(emails.begin(), emails.end());

            for (int i = 0; i < emails.size(); i++) {
                ope::SymbolCode symbol_code = ope::SymbolCode();
                symbol_code.first = emails[i];
                symbol_code.second = ope::Code();
                symbol_code.second.code = i;
                ls.push_back(symbol_code);
            }

            test->build(ls);

            for (int i = 0; i < emails.size() - 1; i++) {
                int prefix_len = -1;
                std::string cur_str = getNextString(emails[i]);
                std::string next_str;
                int next_idx = -1;
                getNextInterval(emails, i, cur_str, next_idx, next_str);
                ope::Code result;
                result = test->lookup(cur_str.c_str(), cur_str.size(), prefix_len);
                if (cur_str.compare(next_str) < 0)
                    ASSERT_TRUE(result.code == i);
                else {
                    // std::cout << cur_str << "\t" << next_str << std::endl;
                    ASSERT_TRUE(result.code == next_idx);
                }
            }
            delete test;
        }

//        TEST_F(ARTDICTest, emailTest) {
//
//        }
//
//        TEST_F (ARTDICTest, insertTest) {
//
//        }
//
//        TEST_F (ARTDICTest, lookupTest) {
//
//        }

        void loadEmails() {
            std::ifstream infile(kEmailFilePath);
            std::string key;
            int count = 0;
            while (infile.good() && count < kEmailTestSize) {
                infile >> key;
                emails.push_back(key);
                count++;
            }
        }

    } // namespace treetest

} // namespace ART_DIC

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);

    ARTDIC::treetest::loadEmails();

    return RUN_ALL_TESTS();
}
