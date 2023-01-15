# 데이터 저장
import collect
from mysql import data_save

df = collect.library_location()
data_save(df, 'library_location')

df = collect.gu_libraries()
data_save(df, 'gu_libraries')

df = collect.gu_materials_per()
data_save(df, 'gu_materials_per')

df = collect.gu_population_per()
data_save(df, 'gu_population_per')

df = collect.gu_librarybudget()
data_save(df, 'gu_librarybudget')

df = collect.library_users()
data_save(df, 'library_users')

df = collect.library_rent()
data_save(df, 'library_rent')

df = collect.gu_population()
data_save(df, 'gu_population')

df = collect.gu_youth_population()
data_save(df, 'gu_youth_population')

df = collect.gu_averageincome()
data_save(df, 'gu_averageincome')

df = collect.gu_satisfaction()
data_save(df, 'gu_satisfaction')

df = collect.gu_household()
data_save(df, 'gu_household')

df = collect.gu_ages()
data_save(df, 'gu_ages')

df = collect.gu_disadv_budget()
data_save(df, 'gu_disadv_budget')

df = collect.gu_disadv_users()
data_save(df, 'gu_disadv_users')

df = collect.gu_schoolage()
data_save(df, 'gu_schoolage')