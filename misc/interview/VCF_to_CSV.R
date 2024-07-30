library(VariantAnnotation)
library(pegas)

vcf_filepath <- "/Users/avyukth/Documents/Learn/UPennGaoLab/vcf_data/sample.vcf"
vcf_data_frame <- VCFloci(vcf_filepath, what="all", chunk.size=1e9, quiet=FALSE)
save_path_Rda <- "/Users/avyukth/Documents/Learn/UPennGaoLab/vcf_data/sample_vcf.Rda"
save_path_csv <- "/Users/avyukth/Documents/Learn/UPennGaoLab/vcf_data/sample_vcf.csv"
saveRDS(vcf_data_frame, file=save_path_Rda)
write.csv(vcf_data_frame, save_path_csv)