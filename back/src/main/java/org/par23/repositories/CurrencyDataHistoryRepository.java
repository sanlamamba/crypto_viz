package org.par23.repositories;

import org.par23.models.CurrencyDataHistory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface CurrencyDataHistoryRepository extends JpaRepository<CurrencyDataHistory, String> {
    Optional<CurrencyDataHistory> findByCurrencyId(String currencyId);

    List<CurrencyDataHistory> findByTimestampBetween(LocalDateTime start, LocalDateTime end);

    List<CurrencyDataHistory> findByCurrencyName(String currencyName);
}