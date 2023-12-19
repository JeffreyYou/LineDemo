package com.jeffrey.linedemo.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import com.jeffrey.linedemo.entity.GreenMessage;

@Repository
public interface MessageRepository extends JpaRepository<GreenMessage, Long> {
    GreenMessage findFirstByOrderByIdAsc();
}